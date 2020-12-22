import React, { useState, useEffect } from "react";
import {
    EmailShareButton,
    EmailIcon,
  } from "react-share";

export default function ShareWidget(props) {
    const [URL, setURL] = useState(window.location.href);
    // const URL_SHORTEN_LINK = process.env.REACT_APP_URL_SHORTENER;

    useEffect(() => {
        setURL(window.location.href)
      }, [])
    
      return (
        <div style={{display: 'flex', justifyContent: 'center'}}>
          <EmailShareButton url={URL}>
            <EmailIcon size={32} round />
          </EmailShareButton>
          </div>
      );
    }
  