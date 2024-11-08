import './Home.css'
import Button from '../../components/Button/Button.js'; 
import ServicesMediaImage from '../../assets/HouseImage2.png'; 
import TestimonialCard from '../../components/TestimonialCard/TestimonialCard';
import { Link } from "react-router-dom";

function Home() {
    return (
        <div className="home-wrapper">
            <div className="hero">
                <div className="hero-content">
                    <h1 className="hero__heading">Welcome to <span className="text-highlight">Vanga Realestate</span></h1>
                    <p className="hero__subtitle">
                        Melbourne-based agency empowering your real estate journey with personalized service and local expertise.
                    </p>
                    <div className="btn-group">
                        <a href="#services">
                            <Button label={"Find Out More"} buttonType={"secondary"} />
                        </a>
                        <Link to="/search">
                            <Button label={"Make A Prediction"} buttonType={"primary"} />
                        </Link>
                    </div>
                </div>
            </div>
            <div id="services" className="services">
                <div className="services-header">
                    <h2 className="services-header__heading">Choose <span className="text-highlight">Vanga</span> As Your Realestate Experts</h2>
                </div>
                <div className="services-wrapper">
                    <div className="services-content">
                        <p className="services-content__text">
                            At Vanga Realestate, we’re committed to helping you find, buy, and sell properties with confidence. Our team combines in-depth market knowledge with cutting-edge technology to simplify your real estate journey. Whether you're exploring neighborhoods or ready to make a move, we offer comprehensive tools to predict the value of your property, empowering you to make informed decisions. Discover your home's potential and make your next steps with us.
                        </p>
                    </div>
                    <div className="services-media">
                        <img className="services-media__image" src={ServicesMediaImage} />
                    </div>
                </div>
            </div>
            <div className="testimonials">
                <div className="testimonials-header">
                    <h2 className="testimonials-header__heading">Testimonials</h2>
                    <p className="testimonials-header__subtitle">
                        Here’s how Vanga Realestate has made a difference for our clients—real stories of successful journeys and happy homes.
                    </p>
                </div>
                <div className="testimonials-wrapper">
                    <TestimonialCard name="Gary" text="
                        They guided me through every step and provided invaluable advice. Highly recommend Vanga Realestate!
                    " 
                    />
                    <TestimonialCard name="Melissa" text="
                        Vanga Realestate helped me find the perfect home in no time. Their expertise made the process easy and stress-free.
                    " 
                    />
                    <TestimonialCard name="David" text="
                        Professional, reliable, and extremely knowledgeable. I couldn’t have asked for a better experience!
                    " 
                    />
                </div>
            </div>
        </div>
    )
}

export default Home; 