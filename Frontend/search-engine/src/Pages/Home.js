import React from "react";

import "./Home.css";

const Home = () => {
  return (
    <React.Fragment>
        <div className="input_div">
          <div className="logo_div">
            Simple Search
          </div>
          <div>
            <input className="input" type="text" id="search_word"></input>
          </div>
          <div className="button_div">
            <button>Search</button>
            <button>Crawl</button>
          </div>
        </div>
    </React.Fragment>
  );
};
  export default Home;