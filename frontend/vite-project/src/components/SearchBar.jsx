import React from "react";

import {FaSearch} from 'react-icons/fa'

export const SearchBar = () => {
    return (
        <div className="input-wrapper">
            <FaSearch className="search-icon" />
            <input type="text" placeholder="Enter your query" />
        </div>
    );
}