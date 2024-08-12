<?php
$username=$_POST['username'];
$email=$_POST['email'];
$password=$_POST['password'];
$RepetPassword=$_POST['RepetPassword'];

if(!empty($username)||!empty($email)||!empty($password)||!empty($RepetPassword))
{
    $host="localhost";
    $dbusername="root";
    $dbpassword="";
    $dbname="login";

    $conn=new mysqli($host,$dbusername,$dbpassword,$dbname);
    if(mysqli_connect_error())
    {
        die('connect Error ('.mysqli_connect_errno().')'.mysqli_connect_error());

    }
    else
    {
        $SELECT="SELECT email From register Where email=? Limit 1";
        $INSERT="INSERT Into register(username,email,password,RepetPassword ) value(?,?,?,?)";

        $stmt=$conn->prepare($SELECT);
        $stmt->bind_param("s",$email);
        $stmt->execute();
        stmt_>bind_result ();
        stmt->store_result();
        $rnum->$stmt->num_rows;

        if(rnum==0)
        {
            $stmt->close();
            $stmt=$conn->prepare($INSERT);
            $stmt->bind_param("ssss",$username,$email,$password,$RepetPassword);
            stmt->execute();
            echo"New Record Inserted Sucessfully";
        }
        else{
            echo"Someone Already Register using this email";
        }
        $stmt->close();
        $conn->close();
    }
    echo"Allfield are required";
    die();
}
?>