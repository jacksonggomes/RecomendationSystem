import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule, 
  MatButtonModule,
  MatIconModule,
  MatSidenavModule,
  MatMenuModule,
  MatListModule
  } from '@angular/material';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    MatCardModule, 
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatMenuModule,
    MatListModule
  ],
  exports: [
    CommonModule,
    MatCardModule, 
    MatButtonModule,
    MatIconModule,
    MatSidenavModule,
    MatMenuModule,
    MatListModule
  ]
})
export class MaterialModule { }
