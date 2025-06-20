"""Articles router implementing CRUD operations for articles."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..auth import get_current_user
from ..database import get_db
from ..db_models import Article as DBArticle, Tag as DBTag, User as DBUser
from ..models import (
    Article,
    ArticlesFeedGetResponse,
    ArticlesGetResponse,
    ArticlesPostRequest,
    ArticlesPostResponse,
    ArticlesSlugGetResponse,
    ArticlesSlugPutRequest,
    ArticlesSlugPutResponse,
    GenericErrorModel,
    Profile,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Articles"])


def _create_article_response(db_article: DBArticle, current_user: DBUser = None) -> Article:
    """Create an Article response from a database Article model.

    Args:
        db_article: The database Article model.
        current_user: The current authenticated user, if any.

    Returns:
        Article: The API response model.
    """
    return Article(
        slug=db_article.slug,
        title=db_article.title,
        description=db_article.description,
        body=db_article.body,
        tagList=[tag.name for tag in db_article.tags],
        createdAt=db_article.created_at,
        updatedAt=db_article.updated_at,
        favorited=current_user is not None and db_article in current_user.favorites,
        favoritesCount=len(db_article.favorited_by),
        author=Profile(
            username=db_article.author.username,
            bio=db_article.author.bio or "",
            image=db_article.author.image or "",
            following=current_user is not None and db_article.author in current_user.following,
        ),
    )


def _get_or_create_tags(db: Session, tag_list: List[str]) -> List[DBTag]:
    """Get existing tags or create new ones.

    Args:
        db: The database session.
        tag_list: List of tag names.

    Returns:
        List[DBTag]: List of Tag models.
    """
    tags = []
    for tag_name in tag_list:
        tag = db.query(DBTag).filter(DBTag.name == tag_name).first()
        if not tag:
            tag = DBTag(name=tag_name)
            db.add(tag)
        tags.append(tag)
    return tags


@router.get(
    "/articles",
    response_model=ArticlesGetResponse,
    responses={"422": {"model": GenericErrorModel}},
    tags=['Articles'],
)
async def get_articles(
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    offset: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(20, ge=1),
    db: Session = Depends(get_db),
    current_user: Optional[DBUser] = Depends(get_current_user),
) -> Union[ArticlesGetResponse, GenericErrorModel]:
    """Get recent articles globally.

    Supports filtering by tag, author, and favorited status.
    Auth is optional.
    """
    logger.info(
        "Fetching articles with filters - tag: %s, author: %s, favorited: %s",
        tag,
        author,
        favorited,
    )

    query = db.query(DBArticle).options(
        joinedload(DBArticle.author),
        joinedload(DBArticle.tags),
        joinedload(DBArticle.favorited_by),
    )

    if tag:
        query = query.join(DBArticle.tags).filter(DBTag.name == tag)
    if author:
        query = query.join(DBArticle.author).filter(DBUser.username == author)
    if favorited:
        query = query.join(DBArticle.favorited_by).filter(DBUser.username == favorited)

    total = query.count()
    articles = query.order_by(DBArticle.created_at.desc())

    if offset:
        articles = articles.offset(offset)
    articles = articles.limit(limit).all()

    logger.info("Found %d articles matching criteria", len(articles))
    return ArticlesGetResponse(
        articles=[_create_article_response(article, current_user) for article in articles],
        articlesCount=total,
    )


@router.post(
    "/articles",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticlesPostResponse,
    responses={"422": {"model": GenericErrorModel}},
    tags=['Articles'],
)
async def create_article(
    body: ArticlesPostRequest,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> Union[ArticlesPostResponse, GenericErrorModel]:
    """Create a new article.

    Auth is required.
    """
    logger.info("Creating new article: %s", body.article.title)

    slug = slugify(body.article.title)
    if db.query(DBArticle).filter(DBArticle.slug == slug).first():
        logger.warning("Article with slug %s already exists", slug)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Article with this title already exists",
        )

    try:
        tags = _get_or_create_tags(db, body.article.tagList or [])

        article = DBArticle(
            slug=slug,
            title=body.article.title,
            description=body.article.description,
            body=body.article.body,
            author=current_user,
            tags=tags,
        )
        db.add(article)
        db.commit()
        db.refresh(article)

        logger.info("Article created successfully: %s", article.slug)
        return ArticlesPostResponse(article=_create_article_response(article, current_user))

    except Exception as e:
        logger.error("Failed to create article: %s", str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create article",
        ) from e


@router.get(
    "/articles/feed",
    response_model=ArticlesFeedGetResponse,
    responses={"422": {"model": GenericErrorModel}},
    tags=['Articles'],
)
async def get_articles_feed(
    offset: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(20, ge=1),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> Union[ArticlesFeedGetResponse, GenericErrorModel]:
    """Get recent articles from users you follow.

    Auth is required.
    """
    logger.info("Fetching articles feed for user: %s", current_user.username)

    query = (
        db.query(DBArticle)
        .join(DBArticle.author)
        .filter(DBArticle.author_id.in_([user.id for user in current_user.following]))
        .options(
            joinedload(DBArticle.author),
            joinedload(DBArticle.tags),
            joinedload(DBArticle.favorited_by),
        )
    )

    total = query.count()
    articles = query.order_by(DBArticle.created_at.desc())

    if offset:
        articles = articles.offset(offset)
    articles = articles.limit(limit).all()

    logger.info("Found %d articles in feed", len(articles))
    return ArticlesFeedGetResponse(
        articles=[_create_article_response(article, current_user) for article in articles],
        articlesCount=total,
    )


@router.get(
    "/articles/{slug}",
    response_model=ArticlesSlugGetResponse,
    responses={"422": {"model": GenericErrorModel}},
    tags=['Articles'],
)
async def get_article(
    slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[DBUser] = Depends(get_current_user),
) -> Union[ArticlesSlugGetResponse, GenericErrorModel]:
    """Get an article by slug.

    Auth is optional.
    """
    logger.info("Fetching article with slug: %s", slug)

    article = (
        db.query(DBArticle)
        .options(
            joinedload(DBArticle.author),
            joinedload(DBArticle.tags),
            joinedload(DBArticle.favorited_by),
        )
        .filter(DBArticle.slug == slug)
        .first()
    )

    if not article:
        logger.warning("Article not found with slug: %s", slug)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    logger.info("Article found: %s", article.slug)
    return ArticlesSlugGetResponse(article=_create_article_response(article, current_user))


@router.put(
    "/articles/{slug}",
    response_model=ArticlesSlugPutResponse,
    responses={"422": {"model": GenericErrorModel}},
    tags=['Articles'],
)
async def update_article(
    slug: str,
    body: ArticlesSlugPutRequest,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> Union[ArticlesSlugPutResponse, GenericErrorModel]:
    """Update an article.

    Auth is required. Only the author can update their articles.
    """
    logger.info("Updating article: %s", slug)

    article = db.query(DBArticle).filter(DBArticle.slug == slug).first()
    if not article:
        logger.warning("Article not found with slug: %s", slug)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    if article.author_id != current_user.id:
        logger.warning(
            "User %s attempted to update article owned by %s",
            current_user.username,
            article.author.username,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the author can update the article",
        )

    try:
        update_data = body.article.dict(exclude_unset=True)
        if "title" in update_data:
            new_slug = slugify(update_data["title"])
            if new_slug != slug and db.query(DBArticle).filter(
                DBArticle.slug == new_slug
            ).first():
                logger.warning("Article with slug %s already exists", new_slug)
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Article with this title already exists",
                )
            update_data["slug"] = new_slug

        for key, value in update_data.items():
            setattr(article, key, value)

        article.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(article)

        logger.info("Article updated successfully: %s", article.slug)
        return ArticlesSlugPutResponse(article=_create_article_response(article, current_user))

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update article: %s", str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update article",
        ) from e


@router.delete(
    "/articles/{slug}",
    response_model=None,
    responses={'422': {'model': GenericErrorModel}},
    tags=['Articles'],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_article(
    slug: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
) -> None:
    """Delete an article.

    Auth is required. Only the author can delete their articles.
    """
    logger.info("Deleting article: %s", slug)

    article = db.query(DBArticle).filter(DBArticle.slug == slug).first()
    if not article:
        logger.warning("Article not found with slug: %s", slug)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    if article.author_id != current_user.id:
        logger.warning(
            "User %s attempted to delete article owned by %s",
            current_user.username,
            article.author.username,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the author can delete the article",
        )

    try:
        db.delete(article)
        db.commit()
        logger.info("Article deleted successfully: %s", slug)
    except Exception as e:
        logger.error("Failed to delete article: %s", str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete article",
        ) from e
