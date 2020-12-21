import './App.css';
import AcogNavBar from './Components/NavBar/navbar';
import {data} from './Data/data';
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
  return (
      <Router>
        <Switch>
          <Route path="/home" render={()=> <Fragment><AcogNavBar title="Remmitance Advice Automation" /><div style={{padding:20}}><CustomTable data={data} title="Remittance" enableclick={true} editable={false}/></div><Footer/></Fragment>}/>
          <Route path="/view/:imgpath" render={(props) => <Fragment><AcogNavBar title="Remmitance Advice Automation" /><View key={props.match.params.imgpath} {...props}/> <Footer/></Fragment>}/>
          <Route path="*" render={()=> <Fragment><AcogNavBar title="Remmitance Advice Automation" /><div style={{padding:20}}><CustomTable data={data} title="Remittance" enableclick={true} editable={false}/></div><Footer/></Fragment>}/>
          
        </Switch>
        </Router>
  );
}

export default App;
