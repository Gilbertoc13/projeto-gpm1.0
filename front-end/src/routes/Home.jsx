import '../index.css';
import CardTrend from '../components/Cards/CardTrend';
import CardsByGenre from '../components/Cards/CardsByGenre';

function Home() {
  
  return (
    <div className="App">
      <CardTrend id="82856" tipo="tv" isMiddlePage={false}/>
      <CardsByGenre title={"Séries em alta"} type={"tv"}/>
      <CardTrend id="693134" tipo="movie" isMiddlePage={true}/>
      <CardsByGenre title={"Filmes em alta"} type={"movie"}/>
    </div>
  );
}

export default Home;
