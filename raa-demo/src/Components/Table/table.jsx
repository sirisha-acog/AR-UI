import React, { useRef, useEffect, useState, Fragment } from 'react';
import { ReactTabulator } from "react-tabulator";
import "react-tabulator/lib/styles.css"; // default theme
// import "react-tabulator/css/semantic-ui/tabulator_semantic-ui.min.css";
import "react-tabulator/css/materialize/tabulator_materialize.min.css";
import "react-image-lightbox/style.css";
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import './table.css';
import DateEditor from "react-tabulator/lib/editors/DateEditor";


export function ARTable(props) {
    console.log(props);
    const column_names = Object.keys(props.data[0])
    // const [imgpath, setImgPath] = useState(null)
    // const [isOpen, setIsOpen] = useState(false);
    // const [rowdata, setrowdata] = useState(null);
    const ref = useRef(null)
    // const rowref = useRef(null)
    var columns = []
    for (var col of column_names) {
        if (col.toLowerCase().includes("amount") === true) {
            columns.push({ title: col.toUpperCase(), field: col, visible: props.showcols !== undefined ? props.showcols[col] : true, headerFilter: "input", hozAlign: 'right', formatter:"money", formatterParams:{
                decimal:".",
                thousand:",",
                precision:false,
            }, editor:props.editable?"input":""})
        }
        else if(col.toLowerCase().includes("status")){
            columns.push({ title: col.toUpperCase(), field: col, headerFilter: "input", visible: props.showcols !== undefined ? props.showcols[col] : (col.includes("path")? false: true), hozAlign: 'center', formatter:"traffic", formatterParams:{
                min:0,
                max:1,
                color:["red", "green"],  
            }, editor:props.editable?"input":"" })
        }
        else if(col.toLowerCase().includes("date")){
            columns.push({ title: col.toUpperCase(), field: col, headerFilter: "input", visible: props.showcols !== undefined ? props.showcols[col] : (col.includes("path")? false: true), hozAlign: 'center', formatter:function(cell, formatterParams, onRendered){
                return formatDate(cell.getValue());
            }, editor:props.editable?DateEditor:"", editorParams:props.editable?{ format: "MM/DD/YYYY" }:{}});
        
        }
        else {
            columns.push({ title: col.toUpperCase(), field: col, headerFilter: "input", visible: props.showcols !== undefined ? props.showcols[col] : (col.includes("path")? false: true), hozAlign: 'center', editor:props.editable?"input":"" });
        }
    }
    console.log(columns)
    useEffect(() => {
        console.log(ref)
        if (ref && ref.current && ref.current.table) {
            ref.current.table.redraw(true)
        }
        
    })
    
    let options = {
        movableColumns: true,
        downloadReady: (fileContents, blob) => {
            return blob
        },
        pagination: "local",
        paginationSize: 10,
        footerElement: "<p>Note: All the amounts are in US dollars</p>"
    };

    const downloadExcel = () => {
        // let xlsx = require("xlsx")

        let fileName = props.title
        if (!('title' in props)) {
            fileName = "export"
        }

        ref.current.table.download('xlsx', `${fileName}.xlsx`, { sheetName: "Data" });

    };
    
    return (
        <div>
            <Button className="btn btn-primary" variant="primary" onClick={downloadExcel} active>
                Export
     </Button>{' '}
     <Button variant="primary" disabled>Share</Button>{' '}
     {props.editable ? <Button className="btn btn-primary" variant="primary" disabled>Save</Button>:<></>}
            <ReactTabulator
                ref={ref}
                layout="fitColumns"
                columns={columns}
                data={props.data}
                options={options}
                rowClick={props.rowClick}
            />
            
        </div>
    )
}


export default function CustomTable(props) {

    const [cols, setCols] = useState({
        "Deposit Date": true,
        "CMG Account Number": false,
        "Lockbox Number": true,
        "Payor": true,
        "Advertiser": false,
        "Payor Account Number": false,
        "Payor Check Number": false,
        "Check Amount": true,
        "Remittance Line Number": false,
        "Invoice Date": true,
        "Invoice Number": true,
        "Period": false,
        "Gross Amount": false,
        "Discount/Adj.": false,
        "Net Amount Paid": true,
        "Status": true,
        "Imagepath": true,
    });
    const rowClick = (e, row) => {
        if (row.getData().Imagepath !== "" && row.getData().Imagepath !== undefined) {
            // setIsOpen(true)
            // setImgPath(row.getData().Imagepath)
            // console.log(imgpath)
            // let row_data = props.data.filter((obj) => obj.Imagepath === row.getData().Imagepath)
            // setrowdata(row_data)
            console.log(row.getData().Imagepath.replaceAll('/', ' '))
            window.open('/view/'+row.getData().Imagepath.replaceAll('/', ' ').trim())
        }
    }

    const [showcols, setShowCols] = useState(cols)

    const handleChecked = (event) => {
        setCols({ ...cols, [event.target.name]: event.target.checked });
    };
    const [open, setOpen] = useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };
    const handleSubmit = () => {
        setShowCols(cols);
        setOpen(false);
    };
    return (
        <Fragment>
            <Button
                className='float-right'
                id="selectColumns"
                size="small"
                variant="primary"
                onClick={handleClickOpen}
                active
            >
                Select Columns
        </Button>
        
            <Modal
                show={open}
                onHide={handleClose}
                aria-labelledby="form-dialog-title"
            >
                <Modal.Header closeButton>
                    <Modal.Title id="form-dialog-title">Columns</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Group id="select">
                            {Object.keys(cols).map((col) => {
                                if (col.toLowerCase().includes("path")) return null;
                                return (
                                    <Form.Check
                                        key={col}
                                        type="switch"
                                        id={col}
                                        className="column"
                                        size="small"
                                        color="primary"
                                        checked={cols[col]}
                                        onChange={handleChecked}
                                        name={col}
                                        label={col}
                                    ></Form.Check>
                                )
                            })}
                        </Form.Group>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={handleSubmit} variant="primary" id="submitbtn" active>
                        Submit
            </Button>
                    <Button onClick={handleClose} variant="secondary" id="closebtn" active>
                        Close
            </Button>
                </Modal.Footer>

            </Modal>
            {' '}
            <ARTable data={props.data} title={props.title} showcols={showcols} rowClick={props.enableclick ?rowClick : ""} editable={props.editable}/>
            {/* <p>Note: All the amounts are in US dollars</p> */}
        </Fragment>
    )
}

function formatDate(date_str){
    let date = new Date(date_str)
  // console.log(date)
  if (date.toString() === "Invalid Date"){
    return date_str
  }
// //   let monthNames = ["Jan", "Feb", "Mar", "Apr",
// //     "May", "Jun", "Jul", "Aug",
// //     "Sep", "Oct", "Nov", "Dec"];
//   let day = date.getDate();

//   let monthIndex = date.getMonth();
// //   let monthName =  monthNames[monthIndex];

//   let year = date.getFullYear();
//   return `${monthIndex}-${day}-${year}`;
var options = {year: 'numeric', month: '2-digit', day: '2-digit'}
return new Intl.DateTimeFormat('en-US', options).format(date)
}