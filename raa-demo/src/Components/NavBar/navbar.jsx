import React from 'react';
import logo from '../../aglogo.svg'
import Navbar from 'react-bootstrap/Navbar';
import './navbar.css'

export default function AcogNavBar(props) {
    return (
        <>
            <Navbar bg="light" variant="light">
                <Navbar.Brand>
                    <a href="https://aganitha.ai">
                        <img
                            alt=""
                            src={logo}
                            className="d-inline-block align-top"
                        /></a>{' '}
    </Navbar.Brand>
    <Navbar.Text id="title"> <a href="/" style={{textDecoration: 'None'}}> Remmitance Advice Automation </a></Navbar.Text>
    <Navbar.Collapse className="justify-content-end">
    <Navbar.Text>
    <a href="#login"><svg xmlns="http://www.w3.org/2000/svg" width="50" height="30" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
</svg>Jane Doe</a>
    </Navbar.Text>
  </Navbar.Collapse>

            </Navbar>
        </>
    )
}
