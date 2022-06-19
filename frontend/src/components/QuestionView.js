import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor() {
    super();
    this.state = {
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
    $.ajax({
      url: `/api/v1/questions?page=${this.state.page}`, //TODO: update request URL
      type: 'GET',
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
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  selectPage(num) {
    this.setState({ page: num }, () => {this.getQuestions(); this.createPagination()});
  }

  createPagination() {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
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
    console.log(id)
    if(id != null || id !=0)
    {
      $.ajax({
        url: `/api/v1/categories/${id}/questions`, //TODO: update request URL
        type: 'GET',
        success: (result) => {
          this.setState({
            questions: result.questions,
            totalQuestions: result.total_questions,
            currentCategory: result.current_category,
          });
          return;
        },
        error: (error) => {
          alert('Unable to load questions. Please try your request again');
          return;
        },
      });
    }else{
      
      return
    }
  };

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/api/v1/questions/search`, //TODO: update request URL
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category,
        });
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again');
        return;
      },
    });
  };

  questionAction = (id) => (action) => {
    if (action === 'DELETE') {
      if (window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/api/v1/questions/${id}`, //TODO: update request URL
          type: 'DELETE',
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again');
            return;
          },
        });
      }
    }
  };

  render() {
    var counter = 0;
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2
            onClick={() => {
              this.getQuestions();
            }}
          >
            Categories
          </h2>
          <ul>
            {
            this.state.categories.map(({id, type}) => {
              const {id: myId, type: myType} = type;
              //console.log(myType.toLowerCase(), id);
              console.log(id, type)
              
              var newList = ["science", "art", "geography", "history", "entertainment", "sports"];
            // if(id >= 1)
            //  counter++;
              
           return   (
              <li
                key={id}
                onClick={() => {
                  this.getByCategory(id);
                }}
              >
                {type}
                {console.log(`${this.state.categories[id]}.svg`)}
                <img
                  className='category'
                  alt={`${type}`}
                  src={`${type}.svg`}
                />
              </li>
            )})}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => {
            const result = this.state.categories[q.category];
            
            console.log(result);
            return(
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={q.categories}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
              pagination={this.createPagination()}
            />
          )})}
          
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
