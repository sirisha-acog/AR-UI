import './App.css';
import AcogNavBar from './Components/NavBar/navbar';
import CustomTable from './Components/Table/table';
// import Container from 'react-bootstrap/Container';
// import Row from 'react-bootstrap/Row';
// import Col from 'react-bootstrap/Col';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Fragment } from 'react';
import { Switch, Route } from "react-router-dom";
import { BrowserRouter as Router } from "react-router-dom";
import View from './Components/View/view';
import Footer from './Components/Footer/footer';

function App() {
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
  return (
      <Router>
        <Switch>
          <Route path="/home" render={()=> <Fragment><AcogNavBar title="Remittance Advice Automation" /><div style={{padding:20}}><CustomTable data={data} title="Remittance" enableclick={true} editable={false}/></div><Footer/></Fragment>}/>
          <Route path="/view/:imgpath" render={(props) => <Fragment><AcogNavBar title="Remmitance Advice Automation" /><View key={props.match.params.imgpath} {...props}/> <Footer/></Fragment>}/>
          <Route path="*" render={()=> <Fragment><AcogNavBar title="Remmitance Advice Automation" /><div style={{padding:20}}><CustomTable data={data} title="Remittance" enableclick={true} editable={false}/></div><Footer/></Fragment>}/>
          
        </Switch>
        </Router>
  );
}

export default App;
