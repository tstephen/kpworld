import { useState } from 'react'
import useSWR from 'swr'
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

const API_URL = 'http://localhost:8000/api/articles?limit=20';

const getAuthToken = () => localStorage.getItem('jwt');

const fetcher = (url) => fetch(url, {
  headers: { 'Authorization': `Token ${getAuthToken()}` }
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
          <li class="nav-item">
            <a class="nav-link" href="/login">Sign in</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/register">Sign up</a>
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
function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch('http://localhost:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user: {
            email,
            password,
          },
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.errors ? Object.values(data.errors).flat().join(', ') : 'Login failed');
      } else {
        // Save token and redirect
        if (data.user && data.user.token) {
          localStorage.setItem('jwt', data.user.token);
        }
        navigate('/');
      }
    } catch (err) {
      setError('Network error');
    }
  };
  return (
    <div className="auth-page">
      <div className="container page">
        <div className="row">
          <div className="col-md-6 offset-md-3 col-xs-12">
            <h1 className="text-xs-center">Sign in</h1>
            <p className="text-xs-center">
              <a href="/register">Need an account?</a>
            </p>
            {error && (
              <ul className="error-messages">
                <li>{error}</li>
              </ul>
            )}
            <form onSubmit={handleSubmit}>
              <fieldset className="form-group">
                <input
                  className="form-control form-control-lg"
                  type="text"
                  placeholder="Email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
              </fieldset>
              <fieldset className="form-group">
                <input
                  className="form-control form-control-lg"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
              </fieldset>
              <button className="btn btn-lg btn-primary pull-xs-right" type="submit">
                Sign in
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Nav />
      <Routes>
        <Route path="/" element={
          <>
            <Banner />
            <Home />
            <Sidebar />
          </>
        } />
        <Route path="/login" element={<Login />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App
