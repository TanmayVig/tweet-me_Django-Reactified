import React, {useEffect, useState} from 'react'
import {loadTweets} from '../lookup'

export function TweetsComponent(props) {

    const textAreaRef = React.createRef()
    const [newTweets, setNewTweets] = useState([])
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        let tempNewTweets = [...newTweets]
        tempNewTweets.unshift({
            id:123123,
            content: newVal,
            likes:0,
        })
        setNewTweets(tempNewTweets)
        textAreaRef.current.value = ''
    }

    return( 
    <div className={props.className}>
        <div className='col-12 mb-3'>
            <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className='form-control' name='tweet'>   
                </textarea>
                <button type='submit' className='btn btn-primary my-3'>Tweet</button>
            </form>
        </div>
        <TweetList newTweets={newTweets}/>
    </div>
    )
}

export function TweetList(props) {
    const [tweetsinit, setTweetsinit] = useState([])
    // console.log(props.newTweets)
    const [tweets, setTweets] = useState([])
    useEffect(()=>{
        const final=[...props.newTweets].concat(tweetsinit)
        // console.log(final)
        if(final.length !== tweets.length){
            setTweets(final)
        }
    },[props.newTweets,tweets,tweetsinit])
    // setTweetsinit(tweets)
    useEffect(() => {
        const myCallback = (response,status) => {
        if(status === 200){
            
            setTweetsinit(response)
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
    const [likes,setLikes] = useState(tweet.likes ? tweet.likes : 0)
    const [userLike,setUserLike] = useState(tweet.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ?action.display: 'Action'
    // console.log(action.type)
    const display = action.type === 'like' ? `${likes} ${action.display}`: actionDisplay
    const handleClick = (event) => {
        event.preventDefault()
        if (action.type === 'like'){
            if(userLike === true){
                setLikes(likes-1)
                setUserLike(false)
            }else{
                setUserLike(true)
                setLikes(likes+1)

            }
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