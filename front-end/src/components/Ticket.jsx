import styles from './Ticket.module.css'
import QR from '../assets/qr-moviemetricks.svg'
import { FaStar } from "react-icons/fa6";

function Ticket({title, rate, backDrop, poster, DiaMes, ano, id}){

    return(
        <div className={styles.DivTicket}>
        <img className={styles.PosterTicket} src={poster} alt="" />
        <div className={styles.TicketDivisor}></div>
        <div>
            <div className={styles.TicketInfos}>
                <div className={styles.TicketBackdrop} style={{ backgroundImage: `url('${backDrop}')` }}>
                    <div className={styles.TicketFade}>
                        <div className={styles.D1}></div>
                        <div className={styles.D2}></div>
                        <h1 className={styles.Title}>{title}</h1>
                    </div>
                </div>
                <div className={styles.RowTicket}>
                        <img className={styles.TicketQR} src={QR} alt="QR Code" />
                        <div className={styles.TicketSeparador} />
                        <div className={styles.TicketDivDates}>
                            <h2>{DiaMes}</h2>
                            <h3>{ano}</h3>
                        </div>
                        <div className={styles.TicketSeparador} />
                        <div className={styles.DivRate}>
                            <h4>{rate}<span>/ 5</span></h4>
                            <FaStar></FaStar>
                        </div>
                </div>
            </div>
        </div>
        </div>
    )

}

export default Ticket