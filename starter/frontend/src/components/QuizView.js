import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;
const baseUrl = "http://127.0.0.1:5000/api/";

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
        quizCategory: null,
        previousQuestions: [], 
        showAnswer: false,
        categories: {},
        numCorrect: 0,
        currentQuestion: {},
        guess: '',
        forceEnd: false
    }
  }

  componentDidMount(){
    var callback = 'c'+Math.floor((Math.random()*100000000)+1);
    $.ajax({
      url: `${baseUrl}categories`,
      type: "GET",
      jsonpCallback: callback,
      dataType: 'json',
      success: (result) => {
        let cats = [];
        for (let i in result.categories) {
          cats[result.categories[i].id] = result.categories[i].type;
        }
        this.setState({ categories: cats })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

  selectCategory = ({type, id=0}) => {
    this.setState({quizCategory: {type, id}}, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }
    var callback = 'c'+Math.floor((Math.random()*100000000)+1);

    $.ajax({
      url: `${baseUrl}quizzes`,
      dataType: 'json',
      jsonpCallback: callback,
      // crossDomain: true,
      contentType: 'application/json',
      type: "POST",
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory.id
      }),
      // xhrFields: {
      //   withCredentials: true
      // },
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [], 
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderPrePlay(){
      return (
          <div className="quiz-play-holder">
              <div className="choose-header">Choose Category</div>
              <div className="category-holder">
                  <div className="play-category" onClick={this.selectCategory}>ALL</div>
                  {Object.keys(this.state.categories).map(id => {
                  return (
                    <div
                      key={id}
                      value={id}
                      className="play-category"
                      onClick={() => this.selectCategory({type:this.state.categories[id], id})}>
                      {this.state.categories[id]}
                    </div>
                  )
                })}
              </div>
          </div>
      )
  }

  renderFinalScore(){
    return(
      <div className="quiz-play-holder">
        <div className="final-header"> Your Final Score is {this.state.numCorrect}</div>
        <div className="play-again button" onClick={this.restartGame}> Play Again? </div>
      </div>
    )
  }

  evaluateAnswer = () => {
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    let evaluate =  this.evaluateAnswer()
    return(
      <div className="quiz-play-holder">
        <div className="quiz-question">{this.state.currentQuestion.question}</div>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">R: {this.state.currentQuestion.answer}</div>
        <div className="next-question button" onClick={this.getNextQuestion}> Next Question </div>
      </div>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer 
        ? this.renderCorrectAnswer()
        : (
          <div className="quiz-play-holder">
            <div className="quiz-question">{this.state.currentQuestion.question}</div>
            <form onSubmit={this.submitGuess}>
              <input id="guess" type="text" name="guess" onChange={this.handleChange}/>
              <input className="submit-guess button" type="submit" value="Submit Answer" />
            </form>
          </div>
        )
  }


  render() {
    return this.state.quizCategory
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
