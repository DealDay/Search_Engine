import React from "react";

import "./ResultItem.css";

const ResultItem = (props) => {
    return (
        <div>
            <a 
            href={props.url}
            target="_blank"
            rel="noreferrer">{props.title}</a>
        </div>
)};

export default ResultItem;