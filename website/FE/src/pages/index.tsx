import Layout from '@/components/layout/layout'

import { FormEvent, useState } from 'react'
import { Button, Card, Input, Select, Option, Dialog, DialogHeader, DialogBody } from '@material-tailwind/react'
import axios, { AxiosResponse } from 'axios'

import { BackendAPIResponse } from '@/components/assets/model'

import { IoCloseSharp } from 'react-icons/io5';
import { ImSpinner8 } from "react-icons/im";

interface IForm {
  //name: string;
  age: number;
  gender: 'Male' | 'Female';
  primary_diagnosis: 'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension';
  num_procedures: number;
  days_in_hospital: number;
  comorbidity_score: number;
  discharge_to: 'Home' | 'Home Health Care' | 'Rehabilitation Facility' | 'Skilled Nursing Facility'
}

interface IResponseData {
  user_id: string;
  is_readmitted: number;
}

interface IResponse {
  status: 'success' | 'error' | 'closed';
  header: string;
  message: string;
}

const defaultResponse: IResponse = {
  status: 'closed',
  header: '',
  message: ''
}

export default function IndexPage() {
  const [name, setName] = useState<string>('');
  const [age, setAge] = useState<number>(0);
  const [primaryDiagnosis, setPrimaryDiagnosis] = useState<'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension' | ''>('');
  const [gender, setGender] = useState<'Male' | 'Female' | ''>('');
  const [numProcedures, setNumProcedures] = useState<number>(0);
  const [daysInHospital, setDaysInHospital] = useState<number>(0);
  const [comorbidityScore, setComorbidityScore] = useState<number>(0);
  const [dischargeTo, setDischargeTo] = useState<'Home' | 'Home Health Care' | 'Rehabilitation Facility' | 'Skilled Nursing Facility' | ''>('');

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<IResponseData | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [formResponse, setFormResponse] = useState<IResponse>(defaultResponse);
  
  const handleDialog = (res: IResponse) => {
      if(res.status === 'closed' || !res) setDialogOpen(false);
      else setDialogOpen(true);
      setFormResponse(res);
  };

  async function handleSubmit(event: FormEvent) {
    try {
      event.preventDefault();

      const data: IForm = {
        //name: name!,
        age: age,
        gender: gender as 'Male' | 'Female',
        primary_diagnosis: primaryDiagnosis as 'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension',
        num_procedures: numProcedures,
        days_in_hospital: daysInHospital,
        comorbidity_score: comorbidityScore,
        discharge_to: dischargeTo as 'Home' | 'Home Health Care' | 'Rehabilitation Facility' | 'Skilled Nursing Facility'
      }

      setLoading(true);
      const result: AxiosResponse = await axios.post(
        `${process.env.NEXT_PUBLIC_BE_URL || 'http://206.189.41.231:4000'}/predict`,
        data
      );

      if(result?.status == 200) {
        setLoading(false);
        setResult(result.data.predictions);
        console.log(result.data);

        handleDialog({
          status: 'success',
          header: 'predict success',
          message: result.data.predictions[0] === 1 ? `Patient will be readmitted. ${result.data.predictions[0]}` : `Patient wont be readmitted. ${result.data.predictions[0]}`
        });
      } else {
        setLoading(false);
        handleDialog({
          status: 'error',
          header: 'failed to send your form',
          message: result.data?.message || ''
        });
      }
    } catch(error: any) {
      setLoading(false);
      handleDialog({
        status: 'error',
        header: 'failed to send your form',
        message: String(error)
      });
    }
  }

  return (
    <Layout title='Admin'>
      <main>
        <div className='min-h-screen h-auto pt-5'>
          <div className='flex flex-col gap-3 items-center justify-center px-[5%]'>
            <h1 className='ptm-h2 text-black font-bold'>Based Hospital</h1>
            <h5 className='ptm-h5 text-gray-800 font-medium'>welcome, Admin!</h5>
          </div>

          <div className='flex flex-col gap-5 justify-center pt-10 md:px-[10%] px-[3%]'>
            <div className='px-[10%]'>
              <Card className='flex flex-col justify-center items-center'>
                <form className='mt-4 mb-2 flex flex-col w-full bg-white rounded-2xl p-5' onSubmit={handleSubmit}>
                  <p className='ptm-card-title text-black pb-3'>Input patient data</p>
                  <div className='mb-1 flex flex-col gap-3 text-black'>
                    
                    <p className='ptm-p2 text-gray-900 font-medium'>Name</p>
                    <Input label='name' className='px-2' value={name as string} onChange={(e) => setName(e.target.value)} crossOrigin={undefined} />

                    <p className='ptm-p2 text-gray-900 font-medium'>Age</p>
                    <Input label='age' className='px-2' value={age as number} onChange={(e) => setAge(Number(e.target.value))} crossOrigin={undefined} />
                    
                    <p className='ptm-p2 text-gray-900 font-medium'>Primary Diagnosis</p>
                    <Select variant='outlined' label='Primary Diagnosis' value={primaryDiagnosis} onChange={(val) => setPrimaryDiagnosis(val as 'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension')}>
                      <Option value='Kidney Disease'>Kidney Disease</Option>
                      <Option value='Diabetes'>Diabetes</Option>
                      <Option value='COPD'>COPD</Option>
                      <Option value='Heart Disease'>Heart Disease</Option>
                      <Option value='Hypertension'>Hypertension</Option>
                    </Select>

                    <p className='ptm-p2 text-gray-900 font-medium'>Gender</p>
                    <Select variant='outlined' label='Gender' value={gender} onChange={(val) => setGender(val as 'Male' | 'Female')}>
                      <Option value='Male'>Male</Option>
                      <Option value='Female'>Female</Option>
                    </Select>

                    <p className='ptm-p2 text-gray-900 font-medium'>Number of Procedures</p>
                    <Input label='num of procedures' className='px-2' value={numProcedures as number} onChange={(e) => setNumProcedures(Number(e.target.value))} crossOrigin={undefined} />

                    <p className='ptm-p2 text-gray-900 font-medium'>Days in Hospital</p>
                    <Input label='days in hospital' className='px-2' value={daysInHospital as number} onChange={(e) => setDaysInHospital(Number(e.target.value))} crossOrigin={undefined} />

                    <p className='ptm-p2 text-gray-900 font-medium'>Comorbidity Score</p>
                    <Input label='comorbidity score' className='px-2' value={comorbidityScore as number} onChange={(e) => setComorbidityScore(Number(e.target.value))} crossOrigin={undefined} />

                    <p className='ptm-p2 text-gray-900 font-medium'>Discharged to</p>
                    <Select variant='outlined' label='Discharged to' value={dischargeTo} onChange={(val) => setDischargeTo(val as 'Home' | 'Home Health Care' | 'Rehabilitation Facility' | 'Skilled Nursing Facility')}>
                      <Option value='Home'>Home</Option>
                      <Option value='Home Health Care'>Home Health Care</Option>
                      <Option value='Rehabilitation Facility'>Rehabilitation Facility</Option>
                      <Option value='Skilled Nursing Facility'>Skilled Nursing Facility</Option>
                    </Select>
                    
                    <Button className='flex mt-3 w-full' fullWidth type='submit'>
                      <span className='ptm-p2 font-bold w-full text-center text-white'>Submit</span>
                    </Button>
                  </div>
                </form>
              </Card>
            </div>
          </div>

          <div>
            <Dialog
                open= {dialogOpen}
                size='lg'
                handler={handleDialog}
                className=' bg-white min-h-[40vh] rounded-2xl'
            >
                <div className='h-full min-h-[40vh] items-start rounded-2xl px-8'>
                    <div className='flex flex-row justify-between items-start'>
                        <DialogHeader className='flex text-black w-[80%]'>
                            <p className='lg:ptm-h2 ptm-h4'>
                                {
                                    formResponse.header
                                }
                            </p>
                        </DialogHeader>
                        <button onClick={() => handleDialog(defaultResponse)} className='p-5'>
                            <IoCloseSharp className=' text-black size-16' />
                        </button>
                    </div>
                    <DialogBody className=' text-black text-left'>
                        <p className='ptm-p4'>
                            {
                                formResponse.message
                            }
                        </p>
                    </DialogBody>
                </div>
            </Dialog>
          </div>
        </div>
      </main>
    </Layout>
  )
}
