import styles from './Separador.module.css'
import Ticket from './Ticket'
import { FaBullhorn } from "react-icons/fa6";

function Separador({nome}){

    return(
        <div className={styles.SeparadorDiv}>
            <h2>{nome}</h2>
            <hr />
        </div>
    )

}

export default Separador