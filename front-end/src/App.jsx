import './App.css';
import NavBar from './components/Layouts/NavBar';
import Footer from './components/Layouts/Footer';
import { Outlet } from 'react-router-dom';

function App() {
  
  return (
    <div className="App">
      <NavBar></NavBar>
      <Outlet></Outlet>
      <Footer></Footer>
    </div>
  );
}

export default App;
