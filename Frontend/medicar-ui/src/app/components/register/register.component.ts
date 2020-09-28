import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/_services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  form = new FormGroup({
    'username': new FormControl(null, [Validators.required, Validators.maxLength(256)]),
    'email': new FormControl(null, [Validators.required, Validators.maxLength(64), Validators.email]),
    'password1': new FormControl(null, [Validators.required, Validators.maxLength(32)]),
    'password2': new FormControl(null, [Validators.required]),
  });
  isSuccessful = false;
  isSignUpFailed = false;
  errorMessage = '';  

  constructor(private authService: AuthService) { }


  ngOnInit() {
  }

  onSubmit() {
    this.authService.register(this.form).subscribe(
      data => {
        this.isSuccessful = true;
        this.isSignUpFailed = false;
      },
      err => {
        this.errorMessage = err.error.message;
        this.isSignUpFailed = true;
      }
    );
  }

}