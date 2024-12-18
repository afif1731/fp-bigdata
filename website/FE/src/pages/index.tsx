import Layout from '@/components/layout/layout'

import { FormEvent, useState } from 'react'
import { Button, Card, Textarea, Input, Select, Option, Dialog, DialogHeader, DialogBody } from '@material-tailwind/react'
import axios, { AxiosResponse } from 'axios'

import { BackendAPIResponse } from '@/components/assets/model'

import { IoCloseSharp } from 'react-icons/io5';
import { ImSpinner8 } from "react-icons/im";

interface IForm {
  name: string;
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
  const [primaryDiagnosis, setPrimaryDiagnosis] = useState<'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension' | ''>('');

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<IResponseData | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [formResponse, setFormResponse] = useState<IResponse>(defaultResponse);
  
  const handleDialog = (res: IResponse) => {
      if(res.status === 'closed' || !res) setDialogOpen(false);
      else setDialogOpen(true);
      setFormResponse(res);
  };

  // async function handleSubmit(event: FormEvent) {
  //   try {
  //     event.preventDefault();

  //     const data: IForm = {
  //       name: name!,
  //       primary_diagnosis: primaryDiagnosis!
  //     }

  //     setLoading(true);
  //     const result: AxiosResponse<BackendAPIResponse<IResponseData>> = await axios.post(
  //       `${process.env.NEXT_PUBLIC_BE_URL || 'http://localhost:4000'}/patient/submit`,
  //       data
  //     );

  //     if(result?.status == 200) {
  //       setLoading(false);
  //       setResult(result.data.data as IResponseData);
  //     } else {
  //       setLoading(false);
  //       handleDialog({
  //         status: 'error',
  //         header: 'failed to send your form',
  //         message: result.data?.message || ''
  //       });
  //     }
  //   } catch(error: any) {
  //     setLoading(false);
  //     handleDialog({
  //       status: 'error',
  //       header: 'failed to send your form',
  //       message: String(error)
  //     });
  //   }
  // }

  return (
    <Layout title='Admin'>
      <main>
        <div className='min-h-screen h-auto pt-5'>
          <div className='flex flex-col gap-3 items-center justify-center px-[5%]'>
            <h1 className='ptm-h2 text-black font-bold animate-spin'>Based Hospital</h1>
            <h5 className='ptm-h5 text-gray-800 font-medium'>welcome, Admin!</h5>
          </div>

          <div className='flex flex-col gap-5 justify-center pt-10 md:px-[10%] px-[3%]'>
            <div className='px-[10%]'>
              <Card className='flex flex-col justify-center items-center'>
                <form className='mt-4 mb-2 flex flex-col w-full bg-white rounded-2xl p-5'>
                  <p className='ptm-card-title text-black pb-3'>Input patient data</p>
                  <div className='mb-1 flex flex-col gap-3 text-black'>
                    
                    <p className='ptm-p2 text-gray-900 font-medium'>Name</p>
                    <Input label='name' className='px-2' value={name as string} onChange={(e) => setName(e.target.value)} crossOrigin={undefined} />
                    
                    <p className='ptm-p2 text-gray-900 font-medium'>Primary Diagnosis</p>
                    <Select variant='outlined' label='Algorithm' value={primaryDiagnosis} onChange={(val) => setPrimaryDiagnosis(val as 'Kidney Disease' | 'Diabetes' | 'COPD' | 'Heart Disease' | 'Hypertension')}>
                      <Option value='Kidney Disease'>Kidney Disease</Option>
                      <Option value='Diabetes'>Diabetes</Option>
                      <Option value='COPD'>COPD</Option>
                      <Option value='Heart Disease'>Heart Disease</Option>
                      <Option value='Hypertension'>Hypertension</Option>
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
