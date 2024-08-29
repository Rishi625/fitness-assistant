import React from "react";

import {FaSearch} from 'react-icons/fa'
import { useState } from 'react'

import './SearchBar.css'

export const SearchBar = () => {
    const [query, setQuery] = useState('');

    const fetchData = () => {
        fetch('https://jsonplaceholder.typicode.com/users')}

    const handleChange = (value) => {
        setQuery(value)
        fetchData(value)
    }

    const handleClick = () => {
        handleChange(query)
    }
    return (

        <div className="input-wrapper">
            <FaSearch className="search-icon" />
            <input 
            type="text" 
            placeholder="Enter your query" 
            value={query} 
            onChange={(e) => setQuery(e.target.value)}/>
            <div className="search-button-container" > <button className="search-button" onClick={handleClick}>Search</button></div>
            <div className='search-results'></div>
        </div>
    );
}

