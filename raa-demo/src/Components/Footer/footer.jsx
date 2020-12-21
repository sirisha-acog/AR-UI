import React, {Fragment} from 'react';
import Navbar from 'react-bootstrap/Navbar';
import './footer.css';
// import ShareWidget from '../Share/share';

export default function Footer(props){
    return(
        <Fragment>
            {/* <ShareWidget/>
            <br/> */}
        <Navbar className="color-nav" variant="light" sticky="bottom">
            <Navbar.Collapse className="justify-content-center">
                <Navbar.Text style={{color:"white"}}>Copyright 2020 Aganitha AI Inc. All rights reserved.</Navbar.Text>
            </Navbar.Collapse>
        </Navbar>
        </Fragment>
    )
}