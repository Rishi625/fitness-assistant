import { useState } from 'react'
import './App.css'
import { SearchBar } from './components/SearchBar'
import { SearchResults } from './components/SearchResults'

function App() {

  return (
      <div className="App">
        <div className="search-bar-container">
          <SearchBar/>
          <div className="search-button"></div>
          </div>
          <div className="search-results-container">
            
          <SearchResults/>
          </div>
      </div>
  )
}

export default App
