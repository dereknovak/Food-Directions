import { useForm } from 'react-hook-form';
import './App.css';

const App = () => {
  return <Form />;
};

const Form = () => {
  const { register, handleSubmit } = useForm();
  return (
    <form onSubmit={handleSubmit((data) => console.log(data))}>
      <label htmlFor="source">Source:</label>
      <input {...register('source')} type="text" />

      <label htmlFor="destination">Destination:</label>
      <input {...register('destination')} type="text" />

      <label htmlFor="context">Additional Info:</label>
      <textarea {...register('context')} />

      <button type="submit">Send</button>
    </form>
  );
};

export default App;
