import { auth } from '@/auth'
import { LoginButtonGithub } from '@/components/login-button-github'
import { LoginButtonGoogle } from '@/components/login-button-google'
import { redirect } from 'next/navigation'

export default async function SignInPage() {
  const session = await auth()
  // redirect to home if user is already logged in
  if (session?.user) {
    redirect('/')
  }
  return (
    <div className="flex h-[calc(100vh-theme(spacing.16))] items-center justify-center py-10">
      <LoginButtonGithub />
      <LoginButtonGoogle />
    </div>
  )
}
