import React, { useState, useEffect } from 'react';
import { FaUser, FaSearch } from 'react-icons/fa';
import styles from './NavBar.module.css';
import logo from '../../assets/icon.png';
import { Link } from 'react-router-dom';

const NavBar = () => {
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        function handleScroll() {
            const scrollPosition = window.scrollY;
            if (scrollPosition > 90) {
                setIsScrolled(true);
            } else {
                setIsScrolled(false);
            }
        }

        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    return (
        <nav className={`${styles.navbar} ${isScrolled ? styles.scrolled : ''}`}>
            <Link to={'/'}>
                <img className={styles.navbarLogo} src={logo} alt="Logo" />
            </Link>
            <div className={styles.navbarIcons}>
                <Link to={'/login'}>
                    <div className={styles.navbarIcon}>
                        <FaUser />
                    </div>
                </Link>
                <div className={styles.navbarSearch}>
                    <Link to={'/search/'}>
                        <FaSearch />
                    </Link>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;
