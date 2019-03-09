import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {

  state = { selectedFile: null }

  fileChangedHandler = event => {
    this.setState({selectedFile: event.target.files[0]})
  }

  uploadHandler = () => {
    console.log(this.state.selectedFile)
    // TODO: Change to client side or other server
    // axios.post('my-domain.com/file-upload', this.state.selectedFile, {
    //   onUploadProgress: progressEvent => {
    //     console.log(progressEvent.loaded / progressEvent.total)
    //   }
    // })
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <p>
            Edit <code>src/App.js</code> and save to reload.
          </p>
         
          <input
            id="diagnostic_image"
            name="diagnostic_image"
            type="file"
            accept="image/png, image/jpeg, image/heic"
            onChange={this.fileChangedHandler}
            alt="diagnostic"
          ></input>

          <button
            onClick={this.uploadHandler}
          > 
            Upload! 
          </button>

        </header>
      </div>
    );
  }
}

export default App;
