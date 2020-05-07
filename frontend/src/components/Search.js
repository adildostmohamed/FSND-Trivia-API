import React, { Component } from "react";

class Search extends Component {
  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch();
  };

  handleInputChange = (event) => {
    this.props.updateQuery(event.target.value);
  };

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          placeholder="Search questions..."
          onChange={this.handleInputChange}
          value={this.props.searchTerm}
        />
        <input type="submit" value="Submit" className="button" />
      </form>
    );
  }
}

export default Search;
