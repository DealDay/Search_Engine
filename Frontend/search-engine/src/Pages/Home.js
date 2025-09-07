import React, { useState } from "react";
import axios from "axios"

import "./Home.css";

const Home = () => {
  const [url, setUrl] = useState('');
  const [tab, setTab] = useState('search'); 
  const [searchWord, setSearchWord] = useState('')

  const switchTab = (evt, tabName) =>{
    var i, tabContent, tabLinks;
    // set display of all tab to none
    tabContent = document.getElementsByClassName('tab_content')
    for(i=0; i<tabContent.length; i++){
      tabContent[i].style.display = "none";
    }
    // set all tab button to not active
    tabLinks = document.getElementsByClassName('tablinks');
    for(i=0; i<tabLinks.length; i++){
      tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }
    // set current tab to active and display content
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active";
  } 

  // const crawl = () => {
  //   axios.post('http://localhost:8000/crawl_web_page', {
  //       'web_page_url': url
  //     }).then(res => {
  //       if (res.data['access_token']) {
  //         // sessionStorage.setItem('token', res.data['access_token']) 
  //         // axios.get(`http://localhost:8000/user/${email}`).then(res => {
  //         //   setUserDetails(res.data) 
  //         //   sessionStorage.setItem('role', res.data['role'])
  //         // })
  //         // setShowLoginPage(false)
  //       }
  //       // else setErr(res.data['error'])
  //     }).catch(() => setSearchWord('Please enter email and password'))
  // };

  // const search = () => {
  //   axios.post('http://localhost:8000/search', {
  //     'key_words': searchWord
  //   }).then(
  //     res => {
  //       if (res.data) {
  //         // sessionStorage.setItem('token', res.data['access_token']) 
  //         // axios.get(`http://localhost:8000/user/${email}`).then(res => {
  //         //   setUserDetails(res.data) 
  //         //   sessionStorage.setItem('role', res.data['role'])
  //         // })
  //         // setShowLoginPage(false)
  //       }}
  //   ).catch(() => setSearchWord('Please enter email and password'))
  // };
  return (
    <React.Fragment>
        <div className="input_div">
          <div className="logo_div">
            Simple Search
          </div>
          <div className="tab_div">
            <button className="tablinks" onClick={event => switchTab(event, 'search')}>Search</button>
            <button className="tablinks" onClick={event => switchTab(event, 'crawl')}>Crawl</button>
          </div>
          <div id="search" className="tab_content">
            <div>
              <input placeholder="&#x1F50D;" className="input" type="text" id="search_word"></input>
            </div>
            <div className="button_div">
              <button>Search</button>
            </div>
          </div>
          <div id="crawl" className="tab_content">
            <div>
              <input placeholder="Please enter a valid url" className="input" type="text" id="url"></input>
            </div>
            <div className="button_div">
              <button>Crawl</button>
            </div>
          </div>
        </div>
    </React.Fragment>
  );
};
export default Home;