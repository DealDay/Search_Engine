import React, { useState, useEffect }  from "react";
import { matchPath, NavLink, useLocation } from "react-router-dom";
import axios from "axios"

import ResultItem from "./ResultItem";

const ResultPage = (props) => {
    const [result, setResult] = useState({});
    const [errorMsg, setErrorMsg] = useState({});
    const searchWord = useLocation().pathname
    const [isLoading, setIsLoading] = useState(true)
    
    useEffect(()=>{
        axios.post('http://localhost:8000/search_the_web', {
        'query': searchWord}).then(res => {
            if (res.data) {
          setResult(res.data)
          setIsLoading(false)
        //   setHomeState(false)
        }}
    ).catch((error) => setErrorMsg(error.message))}, []);

    if (isLoading){
        return(<label>Loading</label>)
    }
    if (!isLoading){
         return (
                <React.Fragment> 
                <div>
                <NavLink style={{color:"black"}} to='/'>SimpleSearch</NavLink>
            </div>
            <ul>
                {result.map((item)=>(
                    <ResultItem
                    url={item.url}
                    title={item.title} />
                ))}
            </ul>
        </React.Fragment>

    )}
   };

export default ResultPage;