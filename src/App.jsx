import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

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
            <div className="article-preview">
              <div className="article-meta">
                <a href="/profile/eric-simons">
                  <img src="http://i.imgur.com/Qr71crq.jpg" />
                </a>
                <div className="info">
                  <a href="/profile/eric-simons" className="author">
                    Eric Simons
                  </a>
                  <span className="date">January 20th</span>
                </div>
                <button className="btn btn-outline-primary btn-sm pull-xs-right">
                  <i className="ion-heart" /> 29
                </button>
              </div>
              <a
                href="/article/how-to-build-webapps-that-scale"
                className="preview-link"
              >
                <h1>How to build webapps that scale</h1>
                <p>This is the description for the post.</p>
                <span>Read more...</span>
                <ul className="tag-list">
                  <li className="tag-default tag-pill tag-outline">realworld</li>
                  <li className="tag-default tag-pill tag-outline">
                    implementations
                  </li>
                </ul>
              </a>
            </div>
            <div className="article-preview">
              <div className="article-meta">
                <a href="/profile/albert-pai">
                  <img src="http://i.imgur.com/N4VcUeJ.jpg" />
                </a>
                <div className="info">
                  <a href="/profile/albert-pai" className="author">
                    Albert Pai
                  </a>
                  <span className="date">January 20th</span>
                </div>
                <button className="btn btn-outline-primary btn-sm pull-xs-right">
                  <i className="ion-heart" /> 32
                </button>
              </div>
              <a href="/article/the-song-you" className="preview-link">
                <h1>
                  The song you won't ever stop singing. No matter how hard you try.
                </h1>
                <p>This is the description for the post.</p>
                <span>Read more...</span>
                <ul className="tag-list">
                  <li className="tag-default tag-pill tag-outline">realworld</li>
                  <li className="tag-default tag-pill tag-outline">
                    implementations
                  </li>
                </ul>
              </a>
            </div>
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
