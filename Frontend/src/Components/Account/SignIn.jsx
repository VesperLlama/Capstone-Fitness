import * as React from "react";
import { AppProvider } from "@toolpad/core/AppProvider";
import { SignInPage } from "@toolpad/core/SignInPage";
import Logo from "../Hero/Header/VIFNXlogo.webp";
import { Button } from "@mui/material";

const providers = [{ id: "credentials", name: "Credentials" }];
const BRANDING = {
  logo: <img src={Logo} alt="Logo" style={{ height: 96 }} />,
  title: "FitFusion",
};

const signIn = async (provider) => {
  const promise = new Promise((resolve) => {
    setTimeout(() => {
      console.log(`Sign in with ${provider.id}`);
      resolve();
    }, 500);
  });
  return promise;
};

export default function SignIn({ switchToSignUp }) {
  return (
    <AppProvider branding={BRANDING}>
      <SignInPage
        signIn={signIn}
        providers={providers}
        slotProps={{ emailField: { autoFocus: true } }}
        slots={{
          signUpLink: () => {
            return <Button onClick={switchToSignUp}>Sign Up</Button>;
          },
        }}
      />
    </AppProvider>
  );
}
