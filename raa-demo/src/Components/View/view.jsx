import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import CustomTable from '../Table/table';

export default function View(props){
    const data =[{
        "Date": [
            "07/16/2020"
        ],
        "Check Number": [
            "000976019"
        ],
        "Invoice Date": [
            "05/31/20",
            "05/31/20",
            "05/31/20"
        ],
        "Invoice Number": [
            "665864-2",
            "682574-2",
            "678813-1"
        ],
        "Gross Amount": [
            "17,525.00",
            "0.00",
            "6,095.00"
        ],
        "Discount": [
            "0.00",
            "0.00",
            "0.00"
        ],
        "Net": [
            "14,896.25",
            "0.00",
            "5,180.75"
        ],
        "Net Less Discount": [
            "14,896.25",
            "0.00",
            "5,180.75"
        ],
        "Gross Total": [
            "23,620.00"
        ],
        "Discount Total": [
            "0.00"
        ],
        "Net Total": [
            "20,077.00"
        ],
        "Net Less Discount Total": [
            "20,977.00"
        ],
        "Imagepath":"images/sample.jpg"
}]
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