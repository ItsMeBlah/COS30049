import './About.css'
import MinhPicture from '../../assets/MinhPicture.jpg';
import SeanPicture from '../../assets/SeanPicture.jpg'; 

function About() {
    return (
        <div className="about-wrapper">
            <div className="about-header">
                <h1 className="about-header__heading">About</h1>
            </div>
            <div className="about-content">
                <div className="bio-card">
                    <div className="bio-card-image-wrapper">
                        <img className="bio-card__image" src={MinhPicture} alt="Picture of Minh"/>
                    </div>
                    <div className="bio-card-header">
                        <h2 className="bio-card-header__heading">Minh Cao</h2>
                    </div>
                    <div className="bio-card-content">
                        <p className="bio-card-content__subtitle">Bachelor of Computer Science at Swinburne University</p>
                        <div className = "bio-card-content-text-wrapper">
                            <p className="bio-card-content__text">
                            Minh Cao is a dedicated computer science student with a passion for technology and innovation. Currently studying at Swinburne University, he is deeply interested in exploring various aspects of computing, including software development, data analysis, and emerging technologies. Minh is known for his curiosity and willingness to tackle challenging problems, which has driven him to engage in various projects that enhance his understanding of the field. Beyond academics, he enjoys collaborating with peers on group projects, where he values teamwork and the exchange of ideas. In his spare time, Minh enjoys reading about the latest trends in technology, participating in online courses, and attending workshops to further expand his knowledge. With a strong foundation in computer science and a commitment to continuous learning, Minh is excited about the future and eager to make a positive impact in the tech industry.
                            </p>
                        </div>
                    </div>
                </div>
                <div className="bio-card">
                    <div className="bio-card-image-wrapper">
                        <img className="bio-card__image" src={SeanPicture} alt="Picture of Sean"/>
                    </div>
                    <div className="bio-card-header">
                        <h2 className="bio-card-header__heading">Sean Smith</h2>
                    </div>
                    <div className="bio-card-content">
                        <p className="bio-card-content__subtitle">Bachelor of Computer Science at Swinburne University</p>
                        <div className = "bio-card-content-text-wrapper">
                            <p className="bio-card-content__text">
                            I am currently pursuing a Bachelor of Computer Science, majoring in Cybersecurity, at Swinburne University. Over the course of my studies, I have developed expertise in web development, Android app development, networking, and AWS cloud services. My coursework has provided a solid foundation in computing and cybersecurity, with practical experience in coding, systems management, and cloud-based solutions. During my third year, I worked in an IT helpdesk role, gaining valuable hands-on experience with real-world IT infrastructure and support processes. This role enhanced my understanding of the technologies businesses use to manage and secure their systems, from network security to troubleshooting enterprise applications. I am passionate about applying my skills to solve complex challenges in cybersecurity and look forward to contributing to the field as I advance my career.
                            </p>
                        </div>
                    </div>
                </div> 
            </div>
        </div>
    )
}

export default About; 