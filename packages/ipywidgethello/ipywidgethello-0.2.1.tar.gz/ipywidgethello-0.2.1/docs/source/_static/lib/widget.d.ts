import { DOMWidgetModel, DOMWidgetView } from '@jupyter-widgets/base';
export declare class ExampleModel extends DOMWidgetModel {
    defaults(): any;
    static serializers: {
        layout: {
            deserialize: (value: any, manager: any) => Promise<any>;
        };
        style: {
            deserialize: (value: any, manager: any) => Promise<any>;
        };
    };
    static model_name: string;
    static model_module: string;
    static model_module_version: string;
    static view_name: string;
    static view_module: string;
    static view_module_version: string;
}
export declare class ExampleView extends DOMWidgetView {
    render(): void;
    value_changed(): void;
}
