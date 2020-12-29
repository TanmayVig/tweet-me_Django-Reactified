import React, {useEffect, useState, UseState} from 'react'
import logo from './logo.svg';
import './App.css';

function loadTweets(callback) {
  const xhr = new XMLHttpRequest()
  const method = "GET"
  const url = "http://localhost:8000/api/tweets"
  const responseType = "json"

  xhr.responseType = responseType
  xhr.open(method, url)
  xhr.onload = function() {
      callback(xhr.response,xhr.status)
  }
  xhr.onerror = function (e) {
    console.log(e)
    callback({'message':'error occurred'},400)
  }
  xhr.send()
}

function App() {
  const [tweets, setTweets] = useState([])

  useEffect(() => {
    const myCallback = (response,status) => {
      console.log(response, status)
      if(status == 200){
        setTweets(response)
      }
    }
    loadTweets(myCallback)
  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          {tweets.map((tweet, index) => {
            return <li>{tweet.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
