import { useForm } from 'react-hook-form';
import './App.css';
import { getRestaurants } from './services/services';
import { useState } from 'react';

const App = () => {
  return (
    <>
      <Header />
      <Main />
      <Footer />
    </>
  );
};

const Header = () => {
  return (
    <header>
      <h1>Food Directions</h1>
      <p>Have a trip? Find some food!</p>
    </header>
  );
};

const Main = () => {
  const [answer, setAnswer] = useState('');

  const handleAcceptAnswer = async (data) => {
    const response = await getRestaurants(data);
    setAnswer(response);
  };

  return (
    <main>
      <Form onSubmit={handleAcceptAnswer} />
      <Response answer={answer} />
    </main>
  );
};

const Form = ({ onSubmit }) => {
  const { register, handleSubmit } = useForm();

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="source">Source:</label>
        <input {...register('source')} type="text" />

        <label htmlFor="destination">Destination:</label>
        <input {...register('destination')} type="text" />
      </div>

      <label htmlFor="context">Additional Info:</label>
      <textarea {...register('context')} />

      <button className="submit" type="submit">
        Send
      </button>
    </form>
  );
};

const Response = ({ answer }) => {
  return (
    <section>
      <pre>{answer}</pre>
    </section>
  );
};

const Footer = () => {
  return <footer>Copyright 2025 NovakCoding Inc</footer>;
};

export default App;
