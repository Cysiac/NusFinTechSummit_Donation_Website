import './Causes.css';
import { useNavigate, Link } from 'react-router-dom';
export default function CausePage({cause}){
    return(
    <div className = 'cause-page'>
        <div className = 'cause-details'>
    <h1>{cause.title}</h1>
    <img src = {cause.imgUrl}></img>
     <div className = 'cause-donate'>
        <h3>Amount raised : {cause.amountFilled} out of {cause.amount}</h3>
        <button className = "donate-button" onClick = {()=> useNavigate(`/special-page`)}>Donate Now</button>
    </div>
   
    </div>
     <p>{cause.description}</p>
    </div>
    );
}