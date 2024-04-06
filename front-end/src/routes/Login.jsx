import '../index.css';
import CadastroLogin from '../components/CadastroLogin/CadastroLogin';

function Login() {
  
  return (
    <div className="App">
        <div style={{height: '100vh', display: 'flex', justifyContent: 'center', backgroundColor: 'var(--corFundo)', width: '100%', flexDirection: 'row'}}>
          <CadastroLogin></CadastroLogin>
        </div>
    </div>
  );
}

export default Login;
