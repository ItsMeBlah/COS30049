import './Button.css';

function Button({ label, onClick, buttonType }) {
    const buttonClass = `btn ${buttonType === 'primary' ? 'btn--is-primary' : 'btn--is-secondary'}`;

    return (
        <button className={buttonClass} onClick={onClick}>
            {label}
        </button>
    );
}

export default Button;