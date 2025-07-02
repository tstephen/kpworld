import { useState } from 'react'
import useSWR from 'swr'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const API_URL = 'http://localhost:8000/api/articles?limit=20';
const AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGRlbW8uY29tIiwiZXhwIjoxNzUxNDUzODYyfQ.4o6iPC_sJ8VXy8titbmlRoM9iCToO5Rvq7IhjA81Q5o';

const fetcher = (url) => fetch(url, {
  headers: { 'Authorization': `Token ${AUTH_TOKEN}` }
}).then(res => res.json());

function Nav() {
  return (
    <nav className="navbar navbar-light">
      <div className="container">
        <a className="navbar-brand" href="/">
          conduit
        </a>
        <ul className="nav navbar-nav pull-xs-right">
          <li className="nav-item">
            {/* Add "active" class when you're on that page" */}
            <a className="nav-link active" href="/">
              Home
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/editor">
              {" "}
              <i className="ion-compose" />
              &nbsp;New Article{" "}
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/settings">
              {" "}
              <i className="ion-gear-a" />
              &nbsp;Settings{" "}
            </a>
          </li>
          <li className="nav-item">
            <a className="nav-link" href="/profile/eric-simons">
              <img src="" className="user-pic" />
              Eric Simons
            </a>
          </li>
        </ul>
      </div>
    </nav>
  )
}

function Footer() {
  return (
    <footer>
      <div className="container">
        <a href="/" className="logo-font">
          conduit
        </a>
        <span className="attribution">
          An interactive learning project from{" "}
          <a href="https://thinkster.io">Thinkster</a>. Code &amp; design licensed
          under MIT.
        </span>
      </div>
    </footer>
  )
}

function Banner() {
  return (
    <div className="banner">
      <div className="container">
        <h1 className="logo-font">conduit</h1>
        <p>A place to share your knowledge.</p>
      </div>
    </div>
  )
}
function Home() {
  return (
    <div className="home-page">
      <div className="container page">
        <div className="row">
          <div className="col-md-9">
            <div className="feed-toggle">
              <ul className="nav nav-pills outline-active">
                <li className="nav-item">
                  <a className="nav-link" href="">
                    Your Feed
                  </a>
                </li>
                <li className="nav-item">
                  <a className="nav-link active" href="">
                    Global Feed
                  </a>
                </li>
              </ul>
            </div>
            <ArticlesList />
            <ul className="pagination">
              <li className="page-item active">
                <a className="page-link" href="">
                  1
                </a>
              </li>
              <li className="page-item">
                <a className="page-link" href="">
                  2
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
function Sidebar() {
  return (
       <div className="col-md-3">
        <div className="sidebar">
          <p>Popular Tags</p>
          <div className="tag-list">
            <a href="" className="tag-pill tag-default">
              programming
            </a>
            <a href="" className="tag-pill tag-default">
              javascript
            </a>
            <a href="" className="tag-pill tag-default">
              emberjs
            </a>
            <a href="" className="tag-pill tag-default">
              angularjs
            </a>
            <a href="" className="tag-pill tag-default">
              react
            </a>
            <a href="" className="tag-pill tag-default">
              mean
            </a>
            <a href="" className="tag-pill tag-default">
              node
            </a>
            <a href="" className="tag-pill tag-default">
              rails
            </a>
          </div>
        </div>
      </div>
  )
}
function ArticlesList() {
  const { data, error, isLoading } = useSWR(API_URL, fetcher);

  if (isLoading) return <div>Loading articles...</div>;
  if (error) return <div>Error loading articles.</div>;
  if (!data || !data.articles) return <div>No articles found.</div>;

  return (
    <div>
      {data.articles.map(article => (
        <div className="article-preview" key={article.slug}>
          <div className="article-meta">
            <a href={`/profile/${article.author.username}`}>
              <img src={article.author.image} alt={article.author.username} />
            </a>
            <div className="info">
              <a href={`/profile/${article.author.username}`} className="author">
                {article.author.username}
              </a>
              <span className="date">{new Date(article.createdAt).toLocaleDateString()}</span>
            </div>
            <button className="btn btn-outline-primary btn-sm pull-xs-right">
              <i className="ion-heart" /> {article.favoritesCount}
            </button>
          </div>
          <a href={`/article/${article.slug}`} className="preview-link">
            <h1>{article.title}</h1>
            <p>{article.description}</p>
            <span>Read more...</span>
            <ul className="tag-list">
              {article.tagList.map(tag => (
                <li className="tag-default tag-pill tag-outline" key={tag}>{tag}</li>
              ))}
            </ul>
          </a>
        </div>
      ))}
    </div>
  );
}
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Nav />
      <Banner/>
      <Home/>
      <Sidebar/>
      <Footer />
    </>
  )
}

export default App
