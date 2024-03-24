import '../index.css';
import CadastroLogin from '../components/CadastroLogin/CadastroLogin';

function Login() {
  
  return (
    <div className="App">
        <div style={{height: '100vh', display: 'flex', justifyContent: 'center', backgroundColor: 'var(--corClaro)', width: '100%'}}>
          <CadastroLogin></CadastroLogin>
        </div>
    </div>
  );
}

export default Login;
