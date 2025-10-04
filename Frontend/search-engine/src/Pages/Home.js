import React, { useState } from "react";
import axios from "axios"
import { NavLink } from "react-router-dom";

import ResultPage from "./ResultPage";
import "./Home.css";

const Home = () => {
  const [webPage, setWebpage] = useState('');
  const [searchWord, setSearchWord] = useState('')
  const [successMsg, setSuccessMsg] = useState('');

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

  const crawl = () => {
    axios.post('http://localhost:8000/crawl_web_page', {
        'url': webPage
      }).then(res => {
        if (res.data) {
          setSuccessMsg(res.data)
        }
        // else setErr(res.data['error'])
      }).catch((error) => setSuccessMsg(error.message))
  };

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
              <input onChange={event => setSearchWord(event.target.value)} 
              placeholder="&#x1F50D;" 
              className="input" type="text" id="search_word"></input>
            </div>
            <div className="button_div">
              <NavLink to={`/${searchWord}`}>Search</NavLink>
            </div>
          </div>
          <div id="crawl" className="tab_content">
            <div>
              <input onChange={event => setWebpage(event.target.value)} 
              placeholder="Please enter a valid url" className="input" type="text" id="url"></input>
            </div>
            <div className="button_div">
              <button onClick={crawl}>Crawl</button>
              <text className="success_msg">{successMsg}</text>
            </div>
          </div>
        </div>
    </React.Fragment>
  );
};
export default Home;