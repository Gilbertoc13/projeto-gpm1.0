import './App.css';
import NavBar from './components/Layouts/NavBar';
import Footer from './components/Layouts/Footer';
import { Outlet } from 'react-router-dom';

function App() {

  function setThemeSoftDark() {
    document.documentElement.style.setProperty('--corFundo', '#14141a');
    document.documentElement.style.setProperty('--corClaro', '#18181f');
    document.documentElement.style.setProperty('--corCinza', '#686e7a');
    document.documentElement.style.setProperty('--corVerde', '#00e486');
  }
  
  function setThemePurple() {
    document.documentElement.style.setProperty('--corFundo', '#1d2133');
    document.documentElement.style.setProperty('--corClaro', '#25293d');
    document.documentElement.style.setProperty('--corCinza', '#686e7a');
    document.documentElement.style.setProperty('--corVerde', '#00e486');
  }
  
  function setThemeDark() {
    document.documentElement.style.setProperty('--corFundo', '#010208');
    document.documentElement.style.setProperty('--corClaro', '#030614');
    document.documentElement.style.setProperty('--corCinza', '#686e7a');
    document.documentElement.style.setProperty('--corVerde', '#00e486');
  }
    
  function setThemeDiscord() {
    document.documentElement.style.setProperty('--corFundo', '#2b333d');
    document.documentElement.style.setProperty('--corClaro', '#313943');
    document.documentElement.style.setProperty('--corCinza', '#686e7a');
    document.documentElement.style.setProperty('--corVerde', '#00e486');
  }
  
  return (
    <div className="App">
      <NavBar></NavBar>
      <Outlet></Outlet>
    </div>
  );
}

export default App;
