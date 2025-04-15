import axios from 'axios';


class App extends React.Component {

  state = {

    todos: []

  };


  componentDidMount() {

    axios.get('http://localhost:8000/api/todos/')

      .then(res => {

        const todos = res.data;

        this.setState({ todos });

      });

  }


  render() {

    return (

      <div>

        {this.state.todos.map(todo => (

          <p key={todo.id}>{todo.title}</p>

        ))}

      </div>

    );

  }

}


export default App;
