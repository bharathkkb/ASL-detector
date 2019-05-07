/**
 * This is the global setup file for tests, automatically configured by CRA.
 */
import { configure } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import puppeteer from 'puppeteer';

configure({ adapter: new Adapter() });
