import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Consulta } from 'src/app/_models/consulta';
import { ConsultaService } from 'src/app/_services/consulta.service';

import {NgbModal, ModalDismissReasons} from '@ng-bootstrap/ng-bootstrap';
import { CreateConsultaComponent } from '../create-consulta/create-consulta.component';
import { TokenStorageService } from 'src/app/_services/token-storage.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  title = 'medicar-ui';
  closeResult = '';
  
  consulta = {} as Consulta
  consultaList: Object

  constructor(
    private consultaService: ConsultaService,
    private createConsultaModal: NgbModal,
    private tokenStorageService: TokenStorageService
) {}
  
  
  ngOnInit() {
    this.getConsultaList();
  }

  logout() {
    this.tokenStorageService.signOut();
  }

  saveConsulta(form: NgForm) {    
    this.consultaService.addConsulta(this.consulta).subscribe(() => {
      this.cleanForm(form);
    });
  }

  getConsultaList() {
    this.consultaService.getConsultaList().subscribe((consultaList: Object) => {
      this.consultaList = consultaList['content'];
    });
  }

  deleteConsulta(consulta: Consulta) {
    this.consultaService.deleteConsulta(consulta).subscribe(() => {
      this.getConsultaList();
    });
  }

  cleanForm(form: NgForm) {
    this.getConsultaList();
    form.resetForm();
    this.consulta = {} as Consulta;
  }

  openAddConsultaModal() {
    this.createConsultaModal.open(
        CreateConsultaComponent
    ).result.then((result) => {
        this.ngOnInit();
     }, (reason) => {
         this.closeResult = `Dismissed ${this.getDismissReason(reason)}`
     })
  }

  private getDismissReason(reason: any): string {
    if (reason === ModalDismissReasons.ESC) {
        return 'by pressing ESC';
    } else if (reason === ModalDismissReasons.BACKDROP_CLICK) {
        return 'by clicking on a backdrop';
    } else {
        return `with: ${reason}`
    }
  }
}
