import React, { Component } from "react";

import "../stylesheets/App.css";
import Question from "./Question";
import Search from "./Search";
import $ from "jquery";

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
      searchTerm: "",
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    const { page, searchTerm, currentCategory } = this.state;
    const searchTermParam = searchTerm !== "" ? `&q=${searchTerm}` : "";
    const categoryParam = currentCategory ? `&category=${currentCategory}` : "";
    console.log(searchTermParam);
    $.ajax({
      url: `/questions?page=${page}${searchTermParam}${categoryParam}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert("Unable to load questions. Please try your request again");
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => this.getQuestions());
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? "active" : ""}`}
          onClick={() => {
            this.selectPage(i);
          }}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  }

  getByCategory = (id) => {
    this.setState({ currentCategory: id }, () => this.getQuestions());
  };

  submitSearch = () => {
    this.getQuestions();
    // $.ajax({
    //   url: `/questions?q=${this.state.searchTerm}&page=${this.state.page}`, //TODO: update request URL
    //   type: "GET",
    //   dataType: "json",
    //   contentType: "application/json",
    //   xhrFields: {
    //     withCredentials: true,
    //   },
    //   crossDomain: true,
    //   success: (result) => {
    //     this.setState({
    //       questions: result.questions,
    //       totalQuestions: result.total_questions,
    //       currentCategory: result.current_category,
    //     });
    //     return;
    //   },
    //   error: (error) => {
    //     alert("Unable to load questions. Please try your request again");
    //     return;
    //   },
    // });
  };

  updateQuery = (searchTerm) => {
    this.setState({ searchTerm });
  };

  questionAction = (id) => (action) => {
    if (action === "DELETE") {
      if (window.confirm("are you sure you want to delete the question?")) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert("Unable to load questions. Please try your request again");
            return;
          },
        });
      }
    }
  };

  renderCategories = () => {
    const { categories } = this.state;
    return categories.map((category) => {
      const { type, id } = category;
      return (
        <li
          key={id}
          onClick={() => {
            this.getByCategory(id);
          }}
        >
          <p>{type}</p>
          <img
            className="category"
            src={`${type}.svg`}
            alt="Backgroud for category"
          />
        </li>
      );
    });
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>{this.renderCategories()}</ul>
          <Search
            updateQuery={this.updateQuery}
            searchTerm={this.state.searchTerm}
            submitSearch={this.submitSearch}
          />
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          <h3>{this.state.totalQuestions} Questions</h3>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories.find(
                (category) => category.id === q.category
              )}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
