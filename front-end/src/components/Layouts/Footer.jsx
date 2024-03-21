import logo from '../../assets/icon.png';
import styles from './Footer.module.css';

function Footer(){
    return (
        <footer>
            <img src={logo} alt="" />
            <div>
                <h2>MovieMetricks</h2>
                <p>&copy; 2024 MovieMetricks</p>
            </div>
            <span></span>
            <div>
                <h3>Sobre</h3>
                <h3>Github</h3>
            </div>
        </footer>
    )
}

export default Footer;