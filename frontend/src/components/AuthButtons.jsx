import { GoogleLogin } from "@react-oauth/google";
import { FaGithub, FaApple } from "react-icons/fa";
import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function AuthButtons() {
  const handleGoogleLogin = async (credentialResponse) => {
    try {
      const res = await axios.post(`${API_BASE}/api/auth/social/google/`, {
        access_token: credentialResponse.credential,
      });
      console.log("✅ Google login success:", res.data);
      // Save JWT token to localStorage for later authenticated requests
      localStorage.setItem("token", res.data.access_token);
      window.location.href = "/dashboard";
    } catch (err) {
      console.error("❌ Google login failed:", err);
    }
  };

  const handleGithubLogin = () => {
    window.location.href = `${API_BASE}/api/auth/github/`;
  };

  const handleAppleLogin = () => {
    window.location.href = `${API_BASE}/api/auth/apple/`;
  };

  return (
    <div className="flex flex-col items-center space-y-4 w-full max-w-sm mx-auto mt-10">
      <GoogleLogin
        onSuccess={handleGoogleLogin}
        onError={() => console.log("Google Login Failed")}
      />

      <button
        onClick={handleGithubLogin}
        className="flex items-center justify-center gap-3 w-full bg-gray-800 text-white py-2 rounded-lg hover:bg-gray-900 transition"
      >
        <FaGithub className="text-xl" />
        Continue with GitHub
      </button>

      <button
        onClick={handleAppleLogin}
        className="flex items-center justify-center gap-3 w-full bg-black text-white py-2 rounded-lg hover:bg-gray-800 transition"
      >
        <FaApple className="text-xl" />
        Continue with Apple
      </button>
    </div>
  );
}