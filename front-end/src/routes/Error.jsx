import '../index.css';
import { Link } from 'react-router-dom';
import Logo from '../assets/icon.png';

function Error() {
    return (
        <div className="App" style={{ height: '100vh', backgroundColor: '#030614' }}>
            <img src={Logo} style={{height: '90px', marginBottom: '25px'}} />
            <h1 style={{ fontSize: '4rem', textAlign: 'center'}}>404</h1>
            <p style={{ textAlign: 'center', marginBlock: '15px' }}>Algo errado aconteceu.</p>
            <div style={{ textAlign: 'center', marginBottom: '25px', backgroundColor: 'transparent'}}>
                <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                    <h2 style={{ padding: '1rem 2rem', fontSize: '1rem', fontFamily: 'montserrat', backgroundColor: 'rgb(6, 12, 38)', borderRadius: '10px'}}>Voltar para Home</h2>
                </Link>
            </div>
        </div>
    );
}

export default Error;