import React, {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'


export function TweetList(props) {
const [tweets, setTweets] = useState([])

useEffect(() => {
    const myCallback = (response,status) => {
    // console.log(response, status)
    if(status === 200){
        setTweets(response)
    }
    }
    loadTweets(myCallback)
},[])
return (tweets.map((tweet, index) => {
    return <Tweet tweet={tweet} key={`${index}-{tweet.id}`} className='my-5 py-5 border bg-white text-dark'/>
}))
}

export function ActionButton(props){
    const {tweet,action} = props
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ?action.display: 'Action'
    // console.log(action.type)
    const display = action.type === 'like' ? `${tweet.likes} ${action.display}`: actionDisplay
    const handleClick = (event) => {
        event.preventDefault()
        if (action.type=== 'like'){
            console.log(tweet.likes+1)
        }
    }
    return <button className={className} onClick={handleClick}>{display}</button>
  }
  
  export function Tweet(props) {
    const {tweet} = props
    const className = props.className ? props.className : "col-10 mx-auto col-md-6"
    return (<div className={className}>
              <p>{tweet.id}-{tweet.content}</p>
              <div className='btn btn-group'>
                <ActionButton tweet = {tweet} action={{type:'like', display:'Likes'}}/>
                <ActionButton tweet = {tweet} action={{type:'unlike', display:'Unlikes'}}/>
                <ActionButton tweet = {tweet} action={{type:'retweet', display:'Retweet'}}/>
              </div>
      </div>)
  }