
import './Home.css';
import { useNavigate, Link } from 'react-router-dom';

function CauseCardList({causesList}){
    return(
        <div className = 'causes-list'>
        {causesList.map(cause =><button onClick = {() => navigate(`/causes/${cause.id}`)}><CauseCard  cause ={cause} /></button> )}
        </div>
    );
}
function CauseCard({cause}){
    return(
        <div className = "cause-card">
           <h3 className = "cause-title">{cause.title}</h3>
            <br/>
            <img src={cause.imgUrl} alt = {cause.title}></img>

        </div>
    );
}
export default function Home({causesList}){
      const navigate = useNavigate();

  const handleViewCauses = () => {
    navigate('/causes');
  };
    return(
        <>
        <h1 className = 'title'>GoFundMe</h1>
        <div className = 'causes'>
            <h2>Causes</h2>

<CauseCardList causesList={causesList} />
            </div>
        </>
    );

}