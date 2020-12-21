import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {data} from '../../Data/data';
import CustomTable from '../Table/table';

export default function View(props){
    const imgpath = decodeURIComponent(props.match.params.imgpath).trim().replaceAll(' ', '/')
    console.log(imgpath)
    const disp_data = data.filter((obj)=> obj.Imagepath.includes(imgpath))
    console.log(disp_data)
    return(
        <Container style={{paddingTop:30, minWidth:"100%"}}>
            <Row>
                <Col xs={12} md={12} sm={10} style={{maxHeight:"50vh", overflowY:"scroll"}}>
            <img src={process.env.PUBLIC_URL+"/"+imgpath} width="60%"  alt="Receipt" className="mx-auto d-block" ></img>
            </Col>
        
            </Row>
            <Row style={{marginTop:30}}>
            <Col xs={12} md={12} sm={10}>
                <CustomTable data={disp_data} columns={Object.keys(disp_data[0])} enableclick={false} editable={true} title="Remittance"/>
                </Col>
                </Row>
        </Container>
    )
}