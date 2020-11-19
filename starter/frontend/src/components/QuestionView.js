import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

const baseUrl = "http://127.0.0.1:5000/api/";

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    var callback = 'c'+Math.floor((Math.random()*100000000)+1);
    $.ajax({
      url: `${baseUrl}questions?page=${this.state.page}`,
      type: "GET",
      jsonpCallback: callback,
      dataType: 'json',
      success: (result) => {
        let cats = [];
        for (let i in result.categories) {
          cats[result.categories[i].id] = result.categories[i].type;
        }
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: cats,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    var callback = 'c'+Math.floor((Math.random()*100000000)+1);
    $.ajax({
      url: `${baseUrl}category/${id}/questions`,
      type: "GET",
      jsonpCallback: callback,
      dataType: 'json',
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `${baseUrl}questions/search`,
      type: "POST",
      dataType: 'json',
      crossDomain: true,
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      // xhrFields: {
      //   withCredentials: true
      // },
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('Are you sure you want to DELETE the question?')) {
        $.ajax({
          url: `${baseUrl}questions/${id}`,
          type: "DELETE",
          dataType: 'json',
          contentType: 'application/json',
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {Object.keys(this.state.categories).map((id, ) => (
              <li key={id} onClick={() => {this.getByCategory(id)}}>
                {this.state.categories[id]}
                <img alt="icon" className="category" src={`${this.state.categories[id].toLowerCase()}.svg`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category]} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
